const express = require('express');
const { MY, SAP } = require('./liveSearch');
const mongoose = require('mongoose');

mongoose.connect('mongodb+srv://dbAdmin:dbAdmin$@creditrating.nijkfp8.mongodb.net/Ratings?retryWrites=true&w=majority', {
    useNewUrlParser: true, useUnifiedTopology: true
});

let db = mongoose.connection;
db.on('error', error => console.log(error));
db.once('open', async () => {
    console.log('Connected to mongodb.');
});

const app = express();
app.use(express.json());
app.use(express.urlencoded({extended: true}));

app.post('/getCompanies', async (req, res) => {
    let payload = req.body.payload;
    let searchMY = await MY.find({$or: [{company: {$regex: new RegExp('^'+payload+'.*',
    'i')}}, {ticker: {$regex: new RegExp('^'+payload+'.*',
    'i')}}]}, null, { limit: 10 }).exec();
    
    // Splice together results here or individual calls for moodys and SP!
    let searchSAP = await SAP.find({$or: [{company: {$regex: new RegExp('^'+payload+'.*',
    'i')}}, {ticker: {$regex: new RegExp('^'+payload+'.*',
    'i')}}]}, null, { limit: 10 }).exec();
    
    result_arr = []; 
    foundSAP = new Set();
    // O(n^2) but n is limited to 10 so currently no need to improve this - todo: improve later
    for (let i = 0; i < searchMY.length; i++) {
        for (let x = 0; x < searchSAP.length; x++) {
            
            if (searchMY[i]["ticker"] == searchSAP[x].ticker) {
                result_arr.push({
                    "company": searchMY[i]["company"],
                    "ticker": searchMY[i]["ticker"],
                    "industry": searchMY[i]["industry"],
                    "ratingsMY": searchMY[i]["ratings"],
                    "ratingsSAP": searchSAP[x]["ratings"]
                });
                foundSAP.add(searchMY[i]["ticker"]);
                break;
            }
        }
        if (!foundSAP.has(searchMY[i]["ticker"])) {
            result_arr.push({
                "company": searchMY[i]["company"],
                "ticker": searchMY[i]["ticker"],
                "industry": searchMY[i]["industry"],
                "ratingsMY": searchMY[i]["ratings"],
                "ratingsSAP": null
            });
        }
    }

    for (let i = 0; i < searchSAP.length; i++) {
        if (!foundSAP.has(searchSAP[i]["ticker"])) {
            result_arr.push({
                "company": searchSAP[i]["company"],
                "ticker": searchSAP[i]["ticker"],
                "industry": searchSAP[i]["industry"],
                "ratingsMY": null,
                "ratingsSAP": searchSAP[i]["ratings"]
            });
        }
    }

    res.send({payload: result_arr.slice(0, 10)});
})

app.post('/getCompanyById', async (req, res) => {
    let payload = req.body.payload;
    let searchMY = await MY.find({_id: payload}).exec();
    res.send({payload: searchMY});
})


app.listen(3000, () => {
    console.log('Server launched on PORT 3000.');
})