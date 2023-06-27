const fs = require('fs');
const moment = require('moment-jalaali');

const date = moment().format('jYYYY/jM/jD');
fs.writeFileSync('date.txt', date);
