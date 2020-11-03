const express = require('express');
let expHandleBars = require('express-handlebars');


let PORT = process.env.PORT || 8080;
let app = express();

app.use(express.static("./public/"));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// ---- handlebars = html injection ----
app.engine('handlebars', expHandleBars({ defaultLayout: "main" }));
app.set('view engine', 'handlebars');

// ---- page routing & api routing ---- 
require("./server/routes/html-routes.js")(app);
// require("./routes/api-routes.js")(app);

app.listen(PORT, function () {
    console.log("Server listening on http://localhost:" + PORT);
});