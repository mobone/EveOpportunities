import { Switch, Route } from "react-router-dom"

import Navbar from "./components/Navbar";
import Homepage from "./pages/Homepage";
import DashboardPage from "./pages/DashboardPage"
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
        <Navbar />
      <Switch>
        <Route exact path="/" component={Homepage} />
        <Route path="/dashboard" component={DashboardPage} />
      </Switch>
    </div>
  );
}

export default App;
