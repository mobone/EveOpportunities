import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";

const useStyles = makeStyles((theme) => ({
    title: {
      flexGrow: 1
    }
    })
);

function Navbar() {
    const classes = useStyles();
    return(
        <AppBar position="static">
            <Toolbar>
            <Typography variant="h5" className={classes.title}>
                EveOpportunities
            </Typography>
            <Button color="inherit">Login</Button>
            </Toolbar>
        </AppBar>
    )
}

export default Navbar;