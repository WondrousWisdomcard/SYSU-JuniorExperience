const Configuration = require('./nodejs-sdk/packages/api').Configuration;
const Web3jService = require('./nodejs-sdk/packages/api').Web3jService;
const createContractClass = require('./nodejs-sdk/packages/api/compile/contractClass').createContractClass;

let config = new Configuration('config.json');
let web3j = new Web3jService(config);

const fs = require('fs');

// 加载智能合约
console.log('Loading contract from compiled file ...');
let compiled = JSON.parse(fs.readFileSync('compiled/SupplyChain.json'))
let contract = createContractClass(
    compiled.name, compiled.abi, compiled.bin, config.encryptType
).newInstance();
console.log('Loading deployed contract address from deployed file ...');
let contractAddr = JSON.parse(fs.readFileSync('deployed/SupplyChain.json'))['contractAddress'];
contract.$load(web3j, contractAddr);
console.log('Done.');

// 准备HTTP服务
const express = require('express');
const bodyParser = require('body-parser');
const port = 9000;
var app = express();
app.use(bodyParser.json({ limit: '10mb'}));
app.use(express.static('web', {index: '/index.html'})); // 网页根目录
function getReqData(req) {
    if (req.body && Object.keys(req.body).length) {
        return req.body;
    }
    if (req.query && Object.keys(req.query).length) {
        return req.query;
    }
    if (req.params && Object.keys(req.params).length) {
        return req.params;
    }
    return {};
}

// 合约方法调用接口参数如下
// account: 字符串，调用合约的账户名，必须是config.json中已有的账户
// method: 字符串，想要调用的合约方法名字
// parameters: 列表，合约方法调用参数
// 返回一个JSON对象字符串
// ok: 布尔值，调用是否成功
// msg: 字符串，如果调用成功，则设为'succeed'，否则为错误信息
// data: 列表，合约方法调用的返回值
app.all('/contractMethod', async (req, res) => {
    let reqData = getReqData(req);
    console.log(`call 'contractMethod' from ip ${req.ip}, params: ${JSON.stringify(reqData)}`);

    if (typeof(reqData.account) != 'string' || typeof(reqData.method) != 'string' ||
        !Array.isArray(reqData.parameters)
    ) { // 检查接口参数类型
        console.log('failed at parameter type checking.');
        res.json({ok: false, msg: 'Bad iterface call.', data: []});
        return;
    }

    // 进行合约方法调用
    try {
        contract.$by(reqData.account);
        let retval = await contract[reqData.method](...reqData.parameters);
        console.log(`retval: ${JSON.stringify(retval)}`);
        res.json({ok: true, msg: 'succeed', data: retval});
    } catch (err) { // 出错
        let errString = err.toString();
        console.log(errString);
        res.json({ok: false, msg: errString, data: []});
    }
});

var server = app.listen(port);
console.log(`server started at port ${port}.`)
