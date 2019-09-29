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

const setDefaultPost = (item, request) => {
  item.createById = request.user._id;
  item.createByUser = request.user.fullname;
  item.createDate = new Date();
  item.updateDate = new Date();
  return item;
};

const setDefaultPut = (item, request) => {
  item.updateById = request.user._id;
  item.updateByUser = request.user.fullname;
  item.updateDate = new Date();
  return item;
};

async function init() {
  try {
    delete User._id;
    const mc = await mongoConnector("evserver", "users");
    const admin = await mc.query.findOne({ username: "admin" });
    if (!admin) await mc.query.insertOne(User);
    mc.connection.close();
  } catch (message) {
    response.json({ error: true, message });
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
    const items = await mc.query
      .find()
      .skip(skip)
      .limit(limit)
      .toArray();
    mc.connection.close();
    response.json({ error: false, items });
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
    const items = await mc.query.find(params).toArray();
    mc.connection.close();
    response.json({ error: false, items });
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
    const { item } = request.body;
    if (db === undefined && collection === undefined && item === undefined) {
      return response.json({
        error: true,
        message: "No enviaste la informacion necesaria"
      });
    }

    const _item = setDefaultPost(item, request);

    const mc = await mongoConnector(db, collection);
    const result = await mc.query.insertOne(_item);
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
    const { items = [] } = request.body;
    if (db === undefined && collection === undefined && items === undefined) {
      return response.json({
        error: true,
        message: "No enviaste la informacion necesaria"
      });
    }
    const _items = items.map(item => setDefaultPost(item));

    const mc = await mongoConnector(db, collection);
    const result = await mc.query.insertMany(_items);
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
    const { item, id } = request.body;
    if (db === undefined && collection === undefined && item === undefined) {
      return response.json({
        error: true,
        message: "No enviaste la informacion necesaria"
      });
    }
    const _item = setDefaultPut(item);
    const mc = await mongoConnector(db, collection);
    const _id = mongo.ObjectID(id);
    const result = await mc.query.updateOne({ _id }, { $set: _item });
    mc.connection.close();
    response.json({ error: false, result });
  } catch (message) {
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

router.get("/image", checkToken, async function(request, response) {
  try {
    const mc = await mongoConnector("evserver", "users");
    const _id = mongo.ObjectID(request.query.id);
    const user = await mc.query.findOne({ _id });
    if (!user)
      return response.json({ error: false, message: "Usuarios no encontrado" });
    response.sendFile(`${__dirname}/assets/images/avatars/${user.avatar}`);
  } catch (messageError) {
    response.json({ error: true, messageError, message: "Ocurrio un error" });
  }
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
