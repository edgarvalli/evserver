const router = require("express").Router();
const mongo = require("mongodb");
const Cryptr = require("cryptr");
const jwt = require("jsonwebtoken");
const secret = "HZcDCHCVT2Mwv66p8JV7nZw9zkHwF4ZSZksF52zjk6XAxjHKzZ";
const cryptr = new Cryptr(secret);

// Model
const User = {
  _id: "",
  email: "edgarvalli80@gmail.com",
  username: "admin",
  fullname: "Administrator",
  password: cryptr.encrypt("admin"),
  dbs: [],
  isAdmin: true,
  token: "",
  avatar: ""
};

const setDefaultPost = (child, request) => {
  child.createById = request.user._id;
  child.createByUser = request.user.fullname;
  child.createDate = new Date();
  child.updateDate = new Date();
  return child;
};

const setDefaultPut = (child, request) => {
  child.updateById = request.user._id;
  child.updateByUser = request.user.fullname;
  child.updateDate = new Date();
  child.createDate = new Date(child.createDate);
  return child;
};

async function init() {
  try {
    delete User._id;
    const mc = await mongoConnector("evserver", "users");
    const admin = await mc.query.findOne({ username: "admin" });
    if (!admin) await mc.query.insertOne(User);
    mc.connection.close();
  } catch (message) {
    // response.json({ error: true, message });
    console.log(message);
  }
}

async function mongoConnector(db, collection) {
  const url = "mongodb://localhost:27017";
  const connection = await mongo.connect(url, {
    useNewUrlParser: true,
    useUnifiedTopology: true
  });

  const query = await connection.db(db).collection(collection);
  return { connection, query };
}

async function checkToken(request, response, next) {
  try {
    const { token } = request.headers;
    if (!token)
      return response.json({ error: true, message: "Token no proporcionado" });

    const decoded = jwt.verify(token, secret);
    request.user = decoded;
    next();
  } catch (errorToken) {
    response.json({
      error: true,
      errorToken,
      message: "Token erroneo o expirado",
      tokenExpired: true
    });
  }
}

router.post("/login", async function(request, response) {
  try {
    const { username, password, autoLogin = false } = request.body;

    const handleError = message => response.json({ error: true, message });
    if (username === undefined)
      return handleError("Debes definir el nombre de usuario o correo");
    if (password === undefined)
      return handleError("Debes definir la contraseña");

    const mc = await mongoConnector("evserver", "users");
    const user = await mc.query.findOne({
      $or: [{ username }, { email: username }]
    });

    if (!user) return handleError("Usuario no encontrado");
    const pass = cryptr.decrypt(user.password);
    if (password !== pass) return handleError("Contraseña incorrecta");
    mc.connection.close();

    delete user.password;
    user.autoLogin = autoLogin;

    user.token = jwt.sign(user, secret, {
      expiresIn: 60 * 60 * 60
    });

    response.json({ error: false, user });
  } catch (message) {
    response.json({ error: true, message });
  }
});

/*
    -This route return all items
    -Is necessary send db and collection param
    -Optional you can send params skip or limit
*/
router.get("/", checkToken, async function(request, response) {
  try {
    const { db = "evserver", collection = "test" } = request.headers;
    let skip = request.query.skip || "0";
    let limit = request.query.limit || "50";
    skip = parseInt(skip);
    limit = parseInt(limit);

    const mc = await mongoConnector(db, collection);
    const data = await mc.query
      .find()
      .skip(skip)
      .limit(limit)
      .sort({ _id: 1 })
      .toArray();
    mc.connection.close();
    response.json({ error: false, data });
  } catch (message) {
    response.json({ error: true, message });
  }
});

/*
    -This route return search result
    -Is necessary send db and collection param, value and props
    -The key props need send the name of the property in the object
        separate with comma (,)
*/
router.get("/search", checkToken, async function(request, response) {
  try {
    const { db = "evserver", collection = "test" } = request.headers;
    const { query } = request;
    const value = query.value || "";
    const props = query.props || "";
    const params = {
      $or: props.split(",").map(prop => {
        return {
          [prop]: new RegExp(value, "i")
        };
      })
    };
    const mc = await mongoConnector(db, collection);
    const data = await mc.query
      .find(params)
      .sort({ _id: 1 })
      .toArray();
    mc.connection.close();
    response.json({ error: false, data });
  } catch (message) {
    response.json({ error: true, message });
  }
});

/*
    -This route store a object into database
    -db, collection, item have to be send by body
*/

router.post("/", checkToken, async function(request, response) {
  try {
    const { db = "evserver", collection = "test" } = request.headers;
    const { child } = request.body;
    if (db === undefined && collection === undefined && child === undefined) {
      return response.json({
        error: true,
        message: "No enviaste la informacion necesaria"
      });
    }

    const _child = setDefaultPost(child, request);

    const mc = await mongoConnector(db, collection);
    const result = await mc.query.insertOne(_child);
    mc.connection.close();
    response.json({ error: false, result });
  } catch (message) {
    response.json({ error: true, message });
  }
});

/*
    -This route store a many object into database
    -db, collection, items have to be send by body
*/

router.post("/insertmany", checkToken, async function(request, response) {
  try {
    const { db, collection } = request.headers;
    const { children = [] } = request.body;
    if (
      db === undefined &&
      collection === undefined &&
      children === undefined
    ) {
      return response.json({
        error: true,
        message: "No enviaste la informacion necesaria"
      });
    }
    const _children = child.map(child => setDefaultPost(item));

    const mc = await mongoConnector(db, collection);
    const result = await mc.query.insertMany(_children);
    mc.connection.close();
    response.json({ error: false, result });
  } catch (message) {
    response.json({ error: true, message });
  }
});

/*
    -This route update a object into database
    -db, collection, item, id have to be send by body
*/

router.put("/", checkToken, async function(request, response) {
  try {
    const { db, collection } = request.headers;
    const { child, id } = request.body;
    if (db === undefined && collection === undefined && child === undefined) {
      return response.json({
        error: true,
        message: "No enviaste la informacion necesaria"
      });
    }
    const _child = setDefaultPut(child, request);
    const mc = await mongoConnector(db, collection);
    const _id = mongo.ObjectID(id);
    const result = await mc.query.updateOne({ _id }, { $set: _child });
    mc.connection.close();
    response.json({ error: false, result });
  } catch (message) {
    console.log(message);
    response.json({ error: true, message });
  }
});

/*
    -This funcion allow to upload image base64
*/

router.put("/upload-image", checkToken, async function(request, response) {
  try {
    const fs = require("fs");
    const { image, id, extension } = request.body;

    // Starting mongo connector
    const mc = await mongoConnector("evserver", "users");
    const _id = mongo.ObjectID(id);
    // Check if user exist
    const user = await mc.query.findOne({ _id });
    if (!user)
      return response.json({ error: false, message: "Usuarios no encontrado" });
    // Remove last avatar
    fs.unlinkSync(`./assets/images/avatars/${user.avatar}`);
    // Store new avatar
    const path = `./assets/images/avatars/${id}.${extension}`;
    fs.writeFileSync(path, image, "base64");
    // Update new name of avatar
    const result = await mc.query.updateOne(
      { _id },
      { $set: { avatar: `${id}.${extension}` } }
    );
    await mc.connection.close();
    response.json({ error: false, message: "success", result });
  } catch (uploadError) {
    response.json({ error: true, message: "unsuccess", uploadError });
  }
});

router.get("/image", async function(request, response) {
  const fs = require("fs");
  const exts = ["png", "jpg", "jpeg", "gif", "tif"];
  let image = "";
  for (let i = 0; i < exts.length; i++) {
    image = `./assets/images/avatars/${request.query.id}.${exts[i]}`;
    if (fs.existsSync(image)) {
      image = `${__dirname}/assets/images/avatars/${request.query.id}.${exts[i]}`;
      break;
    } else {
      image = `${__dirname}/assets/images/avatars/default-avatar.jpg`;
    }
  }
  response.sendFile(image);
});

/*
    -This route detele a object into database
    -db, collection, id as params
*/

router.delete("/", checkToken, async function(request, response) {
  try {
    const { db, collection } = request.headers;
    const { id } = request.query;
    if (db === undefined && collection === undefined && id === undefined) {
      return response.json({
        error: true,
        message: "No enviaste la informacion necesaria"
      });
    }

    const mc = await mongoConnector(db, collection);
    const _id = mongo.ObjectID(id);
    const result = await mc.query.remove({ _id });
    mc.connection.close();
    response.json({ error: false, result });
  } catch (message) {
    response.json({ error: true, message });
  }
});

init();
module.exports = router;
