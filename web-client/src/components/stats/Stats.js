import React,{ useState, useEffect, forwardRef } from 'react';

import '../../assets/css/Stats.css';

export const Stats = forwardRef((props, ref) => {
    const [humidity, setHumidity] = useState(0)
    const [waterTemp, setWaterTemp] = useState(0);
    const [oilTemp, setOilTemp] = useState(0);
    const [interiorTemp, setInteriorTemp] = useState(0);
    const [exteriorTemp, setExteriorTemp] = useState(0);
    const [pressure, setPressure] = useState(0);

    useEffect(() => { setHumidity(props.humidity) }, [props.humidity])
    useEffect(() => { setWaterTemp(props.waterTemp) }, [props.waterTemp])
    useEffect(() => { setOilTemp(props.oilTemp) }, [props.oilTemp])
    useEffect(() => { setInteriorTemp(props.interiorTemp) }, [props.interiorTemp])
    useEffect(() => { setExteriorTemp(props.exteriorTemp) }, [props.exteriorTemp])
    useEffect(() => { setPressure(props.pressure) }, [props.pressure])

    return(
        <div className="stats_container">
            <div className="stats_item">
                <span>Température intérieure:</span>
                <span className="stats_value">{interiorTemp} °C</span>
            </div>
            <div className="stats_item">
                <span>Température extrérieure:</span>
                <span className="stats_value">{exteriorTemp} °C</span>
            </div>
            <div className="stats_item">
                <span>Température eau:</span>
                <span className="stats_value">{waterTemp} °C</span>
            </div>
            <div className="stats_item">
                <span>Température huile:</span>
                <span className="stats_value">{oilTemp} °C</span>
            </div>
            <div className="stats_item">
                <span>Humidité:</span>
                <span className="stats_value">{humidity} %</span>
            </div>
            <div className="stats_item">
                <span>Pression:</span>
                <span className="stats_value">{pressure} Hpa</span>
            </div>
        </div>
    )
});