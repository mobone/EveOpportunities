const express = require('express');
const axios = require('axios');
const cors = require('cors');
let expHandleBars = require('express-handlebars');


let PORT = process.env.PORT || 8080;
let app = express();

app.use(express.static("./public"));
app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// ---- handlebars = html injection ----
app.engine('handlebars', expHandleBars({ defaultLayout: "main" }));
app.set('view engine', 'handlebars');

// ---- page routing & api routing ---- 
require("./server/routes/html-routes.js")(app);
require("./server/routes/api-routes.js")(app);

app.listen(PORT, function () {
    console.log("Server listening on http://localhost:" + PORT);
});
