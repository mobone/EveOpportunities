const express = require('express');
const cors = require('cors');



const PORT = process.env.PORT || 8080;
const app = express();


app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());


// ---- page routing & api routing ----
require("./routes/api")(app);

//app.listen(PORT, function () {
//    console.log("Server listening on http://localhost:" + PORT);
//});
app.listen(3000, '0.0.0.0');
