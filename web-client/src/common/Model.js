import React, { useMemo } from 'react'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'

const Model = ({ url }) => {
    const obj = useMemo(() => new OBJLoader().load(url), [url])
      return <primitive object={obj} />
  }
export default Model