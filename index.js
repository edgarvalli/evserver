const express = require("express");
const app = express();

const PORT = process.env.PORT || 3080;
const limit = "5MB";
app.use(express.json({ limit }));
app.use(express.static("public"));
app.use(express.urlencoded({ extended: false, limit }));
app.use("/evserver", require("./evserver"));
app.listen(PORT, err => {
  if (err) console.log(err);
  console.log(`Server running on port ${PORT}`);
});
