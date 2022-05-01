import React, { Suspense, useEffect, useState, forwardRef } from 'react';
import { Voiture } from './Voiture';
import CameraControls from './CameraControl';
import Loading from './Loading';
import { Canvas } from "react-three-fiber";
import env from "react-dotenv";

import '../../assets/css/Radar.css';

const axios = require('axios');

export const Radar = forwardRef((props, ref) => {

  // Rotation Target
  const [rotation, setRotation] = useState({
    x : 0,
    y : 0,
    z : 0
  })
  
  useEffect(() => { updatePosition(props.gyroPosition) }, [props.gyroPosition])

  const updatePosition = (newPosition) => {
    setRotation({x: newPosition.x/20, y: newPosition.y/20, z: newPosition.z/10})
  }

  const resetGyro = () => {
    setRotation({
      x : 0,
      y: 0,
      z: 0
    })

    axios.get(`${env.api_websocket}/reset-gyro`)
      .then((response) => {
        
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  return (

    <React.Fragment>      
      <Canvas >
        <CameraControls/>
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
        <pointLight position={[-10, -10, -10]} />
        <Suspense fallback={<Loading />}>
          <Voiture rotation={rotation}/>
        </Suspense>
      </Canvas>
      <div className='radar_container' onClick={resetGyro}>
        <div className='bottom' onClick={resetGyro}>
          <span className="content">
            Reset
          </span>
        </div>
      </div>
    </React.Fragment>
    
  );
});
