import React,{ useState } from 'react';
import Axios from 'axios';
import { Spinner } from 'react-bootstrap';
import { AiTwotoneVideoCamera } from "react-icons/ai";


export const Video = () => {

    const [isLoading, setisLoading ] = useState(false)
    const [onError, setonError] = useState(false)
    
    const callPhoto = () => {

        setisLoading(true);
        setonError(false)
        Axios({
            method: "get",
            url: 'http://172.24.1.2:8080/photos',
            timeout: 1000 * 5, 
          })
            .then(result => {

                    setisLoading(false)
                    
            })
            .catch(error => {
              console.log(error);
              console.log("Erreur pas de connexion à l'API Photo")
              setisLoading(false)
              setonError(true)
          });
        
    }

    const DisplayLoading = () => {
        if (isLoading) {
            return ( 
            <div className="content">
            <Spinner  animation="border" role="status">
            </Spinner>
            </div>
           
          )
        }
        else {
           return ( 
           <button className={`content ${onError ? 'error' : ''}`} onClick = {() => callPhoto()} disabled = {isLoading}>
            <AiTwotoneVideoCamera />
           </button>)
        }

    }

    return (
        <div className="video_container">
            <div className="top">
              <img src = "http://172.24.1.2:3000/stream/video.mjpeg" alt = "streaming 4L Avant" />
            </div>
          <div className="button_photo">
            <DisplayLoading/>
          </div>
        </div>
    )
}
