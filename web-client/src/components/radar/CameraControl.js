import React, { useRef } from 'react';
import {useFrame,extend,useThree } from "react-three-fiber";
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
extend({ OrbitControls });

const CameraControls = () => {

  var {
    camera,
    gl: { domElement },
  } = useThree();
  camera.position.set(0,0,15);
  const controls = useRef();
  useFrame((state) => controls.current.update());
  return (
    <orbitControls
      ref={controls}
      args={[camera, domElement]}
      enableZoom={true}
      autoRotate={false}
    />
  );
}

export default CameraControls;
