import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Typography from "@material-ui/core/Typography";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import { Container } from "@material-ui/core";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import Tooltip from "@material-ui/core/Tooltip";

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120
  },
  selectEmpty: {
    marginTop: theme.spacing(2)
  },
  textBox: {
    "& > *": {
      margin: theme.spacing(1),
      width: "25ch"
    }
  },

  table: {
    minWidth: 450
  },
  menuButton: {
    marginRight: theme.spacing(2)
  },
  title: {
    flexGrow: 1
  },
  root: {
    flexGrow: 1
  }
}));

function createData(
  item_name,
  item_type,
  price,
  profit,
  percent,
  volume,
  days
) {
  return { item_name, item_type, price, profit, percent, volume, days };
}

const rows = [
  createData(
    "Large Skill Injector",
    "Pilots Services",
    "606,000,000",
    "114,330,511",
    "18%",
    4,
    15
  )
];

export default function SearchForm() {
  const classes = useStyles();
  const [region, setRegion] = React.useState("");
  const [hub, setHub] = React.useState("");

  const [state, setState] = React.useState({
    checkedCharges: true,
    checkedDrones: true,
    checkedImplants: true,
    checkedServices: true,
    checkedPI: true,
    checkedModules: true,
    checkedEquipment: true,
    checkedShips: true,
    checkedStructures: true,
    checkedProfit: false,
    checkedProfitPercent: false,
    checkedVolume: false,
    checkedDays: false
  });

  const handleRegionChange = (event) => {
    setRegion(event.target.value);
  };

  const handleHubChange = (event) => {
    setHub(event.target.value);
  };

  const handleItemTypeChange = (event) => {
    setState({ ...state, [event.target.name]: event.target.checked });
  };

  return (
    <div>
   
      <div>
        <p></p>
      </div>

      <Container maxWidth="lg">
        <div className={classes.textBox}>
          <Button variant="contained">Hub to Hub</Button>
          <Button variant="contained" color="primary">
            Hub to Region
          </Button>
        </div>
        <div>
          <p></p>
        </div>

        <div>
          <Typography variant="h6" component="h2">
            Region Search
          </Typography>
          <form className={classes.textBox} noValidate autoComplete="off">
            <FormControl className={classes.formControl}>
              <InputLabel id="from-hub-label">From Hub</InputLabel>
              <Select
                labelId="from-hub-label"
                id="from-hub"
                value={hub}
                onChange={handleHubChange}
              >
                <MenuItem value={"jita"}>Jita</MenuItem>
                <MenuItem value={"amarr"}>Amarr</MenuItem>
                <MenuItem value={"rens"}>Rens</MenuItem>
                <MenuItem value={"dodixie"}>Dodixie</MenuItem>
                <MenuItem value={"hek"}>Hek</MenuItem>
              </Select>
            </FormControl>

            <FormControl className={classes.formControl}>
              <InputLabel id="to-region-label">To Region</InputLabel>
              <Select
                labelId="to-region-label"
                id="to-region-select"
                value={region}
                onChange={handleRegionChange}
              >
                <MenuItem value={"Aridia"}>Aridia</MenuItem>
                <MenuItem value={"Black Rise"}>Black Rise</MenuItem>
                <MenuItem value={"Branch"}>Branch</MenuItem>
                <MenuItem value={"Catch"}>Catch</MenuItem>
                <MenuItem value={"Cloud Ring"}>Cloud Ring</MenuItem>
                <MenuItem value={"Cobalt Edge"}>Cobalt Edge</MenuItem>
                <MenuItem value={"Curse"}>Curse</MenuItem>
                <MenuItem value={"Deklein"}>Deklein</MenuItem>
                <MenuItem value={"Delve"}>Delve</MenuItem>
                <MenuItem value={"Derelik"}>Derelik</MenuItem>
                <MenuItem value={"Detorid"}>Detorid</MenuItem>
                <MenuItem value={"Devoid"}>Devoid</MenuItem>
                <MenuItem value={"Domain"}>Domain</MenuItem>
                <MenuItem value={"Esoteria"}>Esoteria</MenuItem>
                <MenuItem value={"Essence"}>Essence</MenuItem>
                <MenuItem value={"Etherium Reach"}>Etherium Reach</MenuItem>
                <MenuItem value={"Everyshore"}>Everyshore</MenuItem>
                <MenuItem value={"Fade"}>Fade</MenuItem>
                <MenuItem value={"Feythabolis"}>Feythabolis</MenuItem>
                <MenuItem value={"Fountain"}>Fountain</MenuItem>
                <MenuItem value={"Geminate"}>Geminate</MenuItem>
                <MenuItem value={"Genesis"}>Genesis</MenuItem>
                <MenuItem value={"Great Wildlands"}>Great Wildlands</MenuItem>
                <MenuItem value={"Heimatar"}>Heimatar</MenuItem>
                <MenuItem value={"Immensea"}>Immensea</MenuItem>
                <MenuItem value={"Impass"}>Impass</MenuItem>
                <MenuItem value={"Insmother"}>Insmother</MenuItem>
                <MenuItem value={"Kador"}>Kador</MenuItem>
                <MenuItem value={"Khanid"}>Khanid</MenuItem>
                <MenuItem value={"Kor-Azor"}>Kor-Azor</MenuItem>
                <MenuItem value={"Lonetrek"}>Lonetrek</MenuItem>
                <MenuItem value={"Malpais"}>Malpais</MenuItem>
                <MenuItem value={"Metropolis"}>Metropolis</MenuItem>
                <MenuItem value={"Molden Heath"}>Molden Heath</MenuItem>
                <MenuItem value={"Oasa"}>Oasa</MenuItem>
                <MenuItem value={"Omist"}>Omist</MenuItem>
                <MenuItem value={"Outer Passage"}>Outer Passage</MenuItem>
                <MenuItem value={"Outer Ring"}>Outer Ring</MenuItem>
                <MenuItem value={"Paragon Soul"}>Paragon Soul</MenuItem>
                <MenuItem value={"Period Basis"}>Period Basis</MenuItem>
                <MenuItem value={"Perrigen Falls"}>Perrigen Falls</MenuItem>
                <MenuItem value={"Placid"}>Placid</MenuItem>
                <MenuItem value={"Pochven"}>Pochven</MenuItem>
                <MenuItem value={"Providence"}>Providence</MenuItem>
                <MenuItem value={"Pure Blind"}>Pure Blind</MenuItem>
                <MenuItem value={"Querious"}>Querious</MenuItem>
                <MenuItem value={"Scalding Pass"}>Scalding Pass</MenuItem>
                <MenuItem value={"Sinq Laison"}>Sinq Laison</MenuItem>
                <MenuItem value={"Solitude"}>Solitude</MenuItem>
                <MenuItem value={"Stain"}>Stain</MenuItem>
                <MenuItem value={"Syndicate"}>Syndicate</MenuItem>
                <MenuItem value={"Tash-Murkon"}>Tash-Murkon</MenuItem>
                <MenuItem value={"Tenal"}>Tenal</MenuItem>
                <MenuItem value={"Tenerifis"}>Tenerifis</MenuItem>
                <MenuItem value={"The Bleak Lands"}>The Bleak Lands</MenuItem>
                <MenuItem value={"The Citadel"}>The Citadel</MenuItem>
                <MenuItem value={"The Forge"}>The Forge</MenuItem>
                <MenuItem value={"The Kalevala Expanse"}>
                  The Kalevala Expanse
                </MenuItem>
                <MenuItem value={"The Spire"}>The Spire</MenuItem>
                <MenuItem value={"Tribute"}>Tribute</MenuItem>
                <MenuItem value={"Vale of the Silent"}>
                  Vale of the Silent
                </MenuItem>
                <MenuItem value={"Venal"}>Venal</MenuItem>
                <MenuItem value={"Verge Vendor"}>Verge Vendor</MenuItem>
                <MenuItem value={"Wicked Creek"}>Wicked Creek</MenuItem>
              </Select>
            </FormControl>

            <TextField
              required
              id="standard-required"
              label="Minimum Profit"
              defaultValue="1,000,000"
            />

            <Button variant="contained" color="primary">
              Search
            </Button>
          </form>
          <div>
            <p></p>
          </div>

          <Typography variant="h6" component="h2">
            Emphasize
          </Typography>
          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedProfit}
                onChange={handleItemTypeChange}
                name="checkedProfit"
                color="primary"
              />
            }
            label="Profit"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedProfitPercent}
                onChange={handleItemTypeChange}
                name="checkedProfitPercent"
                color="primary"
              />
            }
            label="Profit Percent"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedVolume}
                onChange={handleItemTypeChange}
                name="checkedVolume"
                color="primary"
              />
            }
            label="Volume"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedDays}
                onChange={handleItemTypeChange}
                name="checkedDays"
                color="primary"
              />
            }
            label="Days"
          />
          <Typography variant="h6" component="h2">
            Item Types
          </Typography>
          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedCharges}
                onChange={handleItemTypeChange}
                name="checkedCharges"
                color="primary"
              />
            }
            label="Ammunition & Charges"
          />

          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedDrones}
                onChange={handleItemTypeChange}
                name="checkedDrones"
                color="primary"
              />
            }
            label="Drones"
          />

          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedImplants}
                onChange={handleItemTypeChange}
                name="checkedImplants"
                color="primary"
              />
            }
            label="Implants & Boosters"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedServices}
                onChange={handleItemTypeChange}
                name="checkedServices"
                color="primary"
              />
            }
            label="Pilots Services"
          />

          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedPI}
                onChange={handleItemTypeChange}
                name="checkedPI"
                color="primary"
              />
            }
            label="Planetary Infrastructure"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedModules}
                onChange={handleItemTypeChange}
                name="checkedModules"
                color="primary"
              />
            }
            label="Ship and Module Modifications"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedEquipment}
                onChange={handleItemTypeChange}
                name="checkedEquipment"
                color="primary"
              />
            }
            label="Ship Equipment"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedShips}
                onChange={handleItemTypeChange}
                name="checkedShips"
                color="primary"
              />
            }
            label="Ships"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedStructures}
                onChange={handleItemTypeChange}
                name="checkedStructures"
                color="primary"
              />
            }
            label="Structures"
          />
          <div>
            <p> </p>
          </div>
          <div>
            <TableContainer component={Paper} elevation={3}>
              <Table className={classes.table} aria-label="Region Profits">
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>

                    <TableCell align="right">Type</TableCell>
                    <TableCell align="right">Buy Price</TableCell>
                    <TableCell align="right">Profit</TableCell>
                    <TableCell align="right">%</TableCell>
                    <Tooltip title="Volume over the last 30 Days">
                      <TableCell align="right">Volume</TableCell>
                    </Tooltip>
                    <Tooltip title="Number of days sold over the last 30 days">
                      <TableCell align="right">Days Sold</TableCell>
                    </Tooltip>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {rows.map((row) => (
                    <TableRow key={row.item_name}>
                      <TableCell component="th" scope="row">
                        {row.item_name}
                      </TableCell>

                      <TableCell align="right">{row.item_type}</TableCell>
                      <TableCell align="right">{row.price}</TableCell>
                      <TableCell align="right">{row.profit}</TableCell>
                      <TableCell align="right">{row.percent}</TableCell>
                      <TableCell align="right">{row.volume}</TableCell>
                      <TableCell align="right">{row.days}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </div>
        </div>
      </Container>
    </div>
  );
}
