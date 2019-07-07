let express = require('express')
let bodyParser = require('body-parser')
var formidable = require('formidable')
let fs = require('fs')
const { exec } = require('child_process')
let cors = require('cors')

let app = express()
let router = express.Router()
app.use(bodyParser.json({ type: 'application/json' }))
app.use(cors())

let fn = "config.json"
let ft = "filedata.json"

router.get('/load', (req, res) => {
    let js=[]
    let data={}
    if(fs.existsSync(fn)){
        data = JSON.parse(fs.readFileSync(fn, 'utf8'));
    }
    else{
        data={
            recport:'',
            traport:'',
            user:''
        }
    }
    let recport = data.recport;
    let traport = data.traport;
    let v1 = {
    name:"Receiver Port",
    value: recport
    }
    js.push(v1)
    v1 = {
    name:"Transmitter Port",
    value: traport
    }
    js.push(v1)
    res.statusCode=200
    res.json(js)
    res.end()
});

router.get('/portvals', (req, res) => {
    exec("python3 -m serial.tools.list_ports",(err, stdout, stderr) => {
        res.statusCode=200
        let dt = stdout.split('\n')
        dt.pop(dt.length-1)
        for(let i=0; i<dt.length; i++){
          dt[i] = dt[i].trim()
        }
        dx = {data: dt}
        res.json(dx)
        res.end()
    })
});

router.post('/load', (req, res) => {
    let rdata = req.body
    let g = rdata[0]
    let h = rdata[1]
    let traport="",recport=""
    if(h.name=='Transmitter Port'){
        traport=h.value
        recport=g.value
    }
    else{
        traport=g.value
        recport=h.value
    }
    let data = {
        recport,traport
    }
    fs.writeFileSync(fn, JSON.stringify(data))
    res.statusCode=200
    res.end()
});

router.post('/transmit', (req, res) => {
    var form = new formidable.IncomingForm();
    
    let fname=''
    form.parse(req, function (err, fields, files) {
      if(files.filetoupload == undefined){
        res.statusCode = 404
        res.end()
      }
      else{
        var oldpath = files.filetoupload.path;
        fname = files.filetoupload.name;
        var newpath = __dirname + '/' + fname;
        fs.copyFile(oldpath, newpath, function (err) {
          if (err) throw err;
          data = {
              mode:'transmit',
              fname:fname
          }
          fs.writeFileSync(ft, JSON.stringify(data))
          exec("python3 transmit.py",(err, stdout, stderr) => {
              console.log(stdout)
              stderr.trim()
              console.log(stderr)
              if(stderr==''){
                res.statusCode=200
                let dt = JSON.parse(fs.readFileSync(ft, 'utf8'));
                res.json(dt)
                res.end()
              }
              else{
                res.statusCode=500
                res.end()
              }
          })
        })
      }
    })
});

router.post('/receive', (req, res) => {
    let data = {
        mode:'receive'
    }
    fs.writeFileSync(ft, JSON.stringify(data))
    exec("python3 receive.py",(err, stdout, stderr) => {
        console.log(stdout)
        stderr.trim()
        console.log(stderr)
        if(stderr==''){
          res.statusCode=200
          let dt = JSON.parse(fs.readFileSync(ft, 'utf8'));
          res.json(dt)
          res.end()
        }
        else{
          res.statusCode=500
          res.end()
        }
    })
})

var port=30000
app.use('/',router)
var server = app.listen(port)
server.timeout = 0