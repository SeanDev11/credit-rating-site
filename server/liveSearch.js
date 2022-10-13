const mongoose = require('mongoose');

const MYratingsSchema = new mongoose.Schema({
    company: { type: String, required: true },
    ticker: { type: String, required: true },
    industry: { type: String, required: true },
    ratings: { type: Array, "default" : [] }
});

const SAPratingsSchema = new mongoose.Schema({
    company: { type: String, required: true },
    ticker: { type: String, required: true },
    industry: { type: String, required: true },
    ratings: { type: Array, "default" : [] }
});
/*
const CombinedSchema = new mongoose.Schema({
    company: { type: String, required: true },
    ticker: { type: String },
    industry: { type: String },
    ratingsMY: { type: Array, "default" : [] },
    ratingsSAP: { type: Array, "default" : [] }
});*/

// Forcing mongoose to use collection name MY (third argument)

const MY = mongoose.model('MY', MYratingsSchema, 'MY');
const SAP = mongoose.model('SAP', SAPratingsSchema, 'SAP');

module.exports = { MY, SAP };
