import React from "react";
import { Link } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";

import { AppBar, Container, Toolbar, IconButton, List, ListItem, ListItemText } from "@material-ui/core"
import { Home } from "@material-ui/icons"
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";

const useStyles = makeStyles({
    navDisplayFlex: {
      display: `flex`,
      justifyContent: `flex-end`
      
    },
    linkText: {
      textDecoration: `none`,
      textTransform: `uppercase`,
      color: `white`
    }
  });


function Navbar() {
    const classes = useStyles();
    const navLinks = [
        { title: `Home`, path: `/` },
        { title: `login`, path: `/login` },
        { title: `dashboard`, path: `/dashboard` },
      ]

    return(
        <AppBar position="static">
            <Toolbar>
                <Container maxWidth="md" className={classes.navbarDisplayFlex}>
                    <List  
                        component="nav"
                        aria-labelledby="main navigation"
                        className={classes.navDisplayFlex}
                    >
                        {navLinks.map(({ title, path }) => (
                        <Link to={path} key={title} className={classes.linkText}>
                            <ListItem button>
                                <ListItemText primary={title} />
                            </ListItem>
                        </Link>
                        ))}
                    </List>
                </Container>
            </Toolbar>
        </AppBar>
    )
}

export default Navbar;