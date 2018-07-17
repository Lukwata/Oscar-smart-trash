var Express = require('express');
var multer = require('multer');
var bodyParser = require('body-parser');
var path = require('path');
const exec_cmd = require('child_process').exec;
    
fs = require('fs');
sys = require('sys');

var app = Express(); 

app.use(bodyParser.json({
    limit: '16mb'
}));

app.use(bodyParser.urlencoded({
    extended: false,
    limit: '16mb'
}));

var cors = require('cors')
app.use(cors());
app.use(function (req, res, next) {
    
        // Website you wish to allow to connect
        
        res.setHeader('Access-Control-Allow-Origin', "*"); 
        // Request methods you wish to allow
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    
        // Request headers you wish to allow
        res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    
        // Set to true if you need the website to include cookies in the requests sent
        // to the API (e.g. in case you use sessions)
        res.setHeader('Access-Control-Allow-Credentials', true);
    
        // Pass to next layer of middleware
        next();
    });


app.use(Express.static(__dirname + '/statics'));

var Storage = multer.diskStorage({
    destination: function(req, file, callback) {
        callback(null, "./Images");
    },
    filename: function(req, file, callback) {
        callback(null, file.fieldname + "_" + Date.now() + "_" + file.originalname);
    }
});

var upload = multer({
    storage: Storage
}).array("imgUploader", 1); //Field name and max count
 
app.get("/", function(req, res) {
    res.sendFile(__dirname + "/index.html");
});
app.post("/api/Upload", function(req, res) {
    
    var matches = req.body.imgUploader.match(/^data:.+\/(.+);base64,(.*)$/);
    var buffer = new Buffer(matches[2], 'base64');

    var classtrash = req.body.trashtype; 

    var trashdir = path.resolve(__dirname + '/images/'+classtrash);

    if (!fs.existsSync(trashdir)){
        fs.mkdirSync(trashdir);
    }
    var tmpName = new Date().toISOString().replace(/[-T:\.Z]/g, "") 
    // top : c0,
    //left : c1,
    // right: c2,
    // format : datetime_pos.jpg
    var savePath = path.resolve(__dirname + '/images/'+classtrash +'/'+ tmpName +'_c0.jpg');
    console.log(savePath); 
    try {
        fs.writeFileSync(savePath, buffer);
        let camleft = "sudo fswebcam -d /dev/video0 -r 640x480 --no-banner "+__dirname + '/images/'+classtrash+"/"+tmpName +"_c1.jpg";
        let camright = "sudo fswebcam -d /dev/video1 -r 640x480 --no-banner "+__dirname + '/images/'+classtrash+"/"+tmpName +"_c2.jpg";
 
        exec_cmd(camleft, (error, stdout, stderr) =>{ console.log(stdout)})
        exec_cmd(camright, (error, stdout, stderr) =>{ console.log(stdout)})

        res.json({ status: 1  });
    } catch (error) {
        console.log(error);
        res.json({ status: 0  });

    } 
   

});
 

// Sau Khi Co Image -> Upload Server ---> S3 -> save Database DynamoDB
// app.post('/api/Upload',  function(req, res){
//     //var buff = new Buffer(req.body.a.replace(/^data:image\/\w+;base64,/,""),'base64');
//     // var buff = new Buffer(req.body.imgUploader,'base64');
//     // var nameurl = rand.generate() + '.jpg';
    
//     console.log(req.body.img);
//     return res.end("File uploaded sucessfully!.");
// });

// var options = {
//   key: fs.readFileSync(path.resolve(__dirname +'/server.key')),
//   cert: fs.readFileSync(path.resolve(__dirname +'/server.pem'))
// }; 

// var https = require('https');
// https.createServer(options, app).listen(3000);

app.listen(2000, function(a) {
    console.log("Listening to port 2000");
});
