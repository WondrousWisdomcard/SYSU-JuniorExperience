const Configuration = require('./nodejs-sdk/packages/api').Configuration;
const CompileService = require('./nodejs-sdk/packages/api').CompileService;
const Web3jService = require('./nodejs-sdk/packages/api').Web3jService;
const createContractClass = require('./nodejs-sdk/packages/api/compile/contractClass').createContractClass;

let config = new Configuration('config.json');
let web3j = new Web3jService(config);

const readline = require('readline');
const fs = require("fs");

async function input(query) {
    let rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    return new Promise((resolve, reject) => {
        rl.question(query, (res) => {
            rl.close();
            resolve(res);
        });
    });
}

async function main() {
    //编译合约
    let compServ = new CompileService(config);
    let name = 'SupplyChain';
    console.log('Compiling the contract: SupplyChain');
    let contractClass = compServ.compile(`contracts/${name}.sol`);
    console.log('Compilation finished.');
    fs.writeFile(`compiled/${name}.json`, JSON.stringify(contractClass), (err) => {
        if (err) {
            console.log('Failed to wirte compiled file.');
            console.log(err);
        }
    });
    
    //认证机构ca部署合约
    let account = 'ca';
    let compiled = JSON.parse(JSON.stringify(contractClass));
    let contract = createContractClass(compiled.name, compiled.abi, compiled.bin, config.encryptType).newInstance();
    let parameters = [];
    console.log(`Deploy contract ${name} using account ca`);
    try {
        let res = await web3j.deploy(compiled.abi, compiled.bin, parameters, account);
        fs.writeFile(`deployed/${name}.json`, JSON.stringify(res), (err) => {
            if (err) {
                console.log('Contract deployed, but failed to write deployed file.');
                console.log(err);
            }
        });
    } catch(err) {
        console.log('Failed.');
        console.log(err);
    }

    //使用认证机构ca注册car bank tyre hub四个公司，需手动输入信息，companyAddr见web/client.js
    let company = await input('Which company are you gonna regist? If none, input .exit:');
    let contractAddr = JSON.parse(fs.readFileSync(`deployed/${name}.json`))['contractAddress'];
    contract.$load(web3j, contractAddr);
    let companyAddr;
    let balance = 0;
    let companyType = 0;
    while(company!='.exit'){
        companyAddr = await input('input the company´address:');
        balance = await input('input the company´balance:');
        companyType =  await input('input the company´companyType(1-金融机构 / 2-核心企业 / 3-下游企业):');
        try {
            contract.$by(account);
            let parameters = [companyAddr,company,balance,companyType];
            let re_res = await contract['registerCompany'](...parameters);
            console.log(re_res);
        } catch(err) {
            console.log('error occurred.');
            console.log(err);
        }
        company = await input('Which company are you gonna regist? If none, input .exit:');
    }    
}

main();