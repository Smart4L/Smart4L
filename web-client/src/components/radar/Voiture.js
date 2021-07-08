import React,{useRef,useState} from  "react";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import voiture_3d from "../../assets/Modele/voiture3.glb";
import {useLoader,useFrame} from "react-three-fiber";

// entre les parenthee tu met toutes tes props,
export const Voiture = ({ rotation }) => {
  const mesh = useRef()
  const nodes = useLoader(GLTFLoader, voiture_3d);
 
  const state = useState({

    axe_x : 0,

  })

   useFrame(() => {

    // Augmentation Axe X
     if(mesh.current.rotation.x != rotation.x) {
      mesh.current.rotation.x = rotation.x;
     }
    // Augmentation Axe Z
     if(mesh.current.rotation.z != rotation.z) {
      mesh.current.rotation.z = rotation.z;
     }

   })
   

  return (
    <group>
      <mesh visible geometry={nodes.nodes.Mesh_0.geometry}  ref={mesh}>
        <meshStandardMaterial
          attach="material"
          color="blue"
          roughness={0.4}
          metalness={0.1}
        />
      </mesh>
    </group>
  );


  
}






