import "./App.css";
import React, { useState, useEffect } from "react";
import { Deploy } from "./component/Deploy/Deploy";

function App() {
  const [state, setState] = useState([]);

  useEffect(() => {
    fetch("/api")
      .then((response) => {
        if (response.status === 200) {
          return response.json();
        }
      })
      .then((data) => setState(data))
      .then((error) => console.log(error));
  }, []);

  return (
    <div className="App">
      <Deploy state={state} />
    </div>
  );
}

export default App;
