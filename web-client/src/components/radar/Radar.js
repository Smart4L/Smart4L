import React, { Suspense,  useState } from 'react';
import { Voiture } from './Voiture';
import CameraControls from './CameraControl';
import Loading from './Loading';
import { Canvas} from "react-three-fiber";


export const Radar = ({propsName}) =>
{

  // Rotation Target
  const [rotation, setRotation] = useState({
    x : 0,
    y : 0,
    z : 0
  })
  
  const generateur = () => {
    const min = 1;
    const max = 100;
    const rand = min + Math.random() * (max - min);
  //  this.setRandom( random + rand );
  }

   return (

     <React.Fragment>
     <button onClick={() => setRotation({
       x : rotation.x+0.01,
       y: rotation.y,
       z: rotation.z
     })}>
        Axe X+
      </button>
      <button onClick={() => setRotation({
       x : rotation.x-0.01,
       y: rotation.y,
       z: rotation.z
     })}>
        Axe X-
      </button>
      <button onClick={() => setRotation({
       x : rotation.x,
       y: rotation.y,
       z: rotation.z+0.01
     })}>
        Axe Z+
      </button>
      <button onClick={() => setRotation({
       x : rotation.x,
       y: rotation.y,
       z: rotation.z-0.01
     })}>
        Axe Z-
      </button>

      <button onClick={() => setRotation({
       x : 0,
       y: 0,
       z: 0
     })}>
        Reset
      </button>

      <Canvas >
      <CameraControls/>
      <ambientLight intensity={0.5} />
      <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
      <pointLight position={[-10, -10, -10]} />
      <Suspense fallback={<Loading />}>
        <Voiture rotation={rotation}/>
      </Suspense>
    </Canvas>
     </React.Fragment>
    
  );
}
