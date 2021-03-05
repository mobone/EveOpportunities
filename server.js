if (process.env.NODE_ENV !== "production") {
   require("dotenv").config();
 }
 
const express = require('express');
const cors = require('cors');



const PORT = process.env.PORT || 8080;
const app = express();


app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());


// ---- page routing & api routing ----
require("./routes/api")(app);


if (process.env.NODE_ENV === "production") {
   app.use(express.static("client/build"));
 
   app.get("*", function (req, res) {
     res.sendFile(path.join(__dirname, "client/build", "index.html"));
   });
 }

app.listen(PORT, function () {
   console.log("Server listening on http://localhost:" + PORT);
});

