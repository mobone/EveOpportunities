import { Switch, Route } from "react-router-dom"
import Dashboard from "./components/Dashboard.js";
import Homepage from "./pages/Homepage";
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <Switch>
        <Route exact path="/" component={Dashboard} />
      </Switch>
    </div>
  );
}

export default App;
