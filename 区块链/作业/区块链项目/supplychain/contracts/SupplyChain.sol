pragma solidity >=0.4.22 <0.6.11;
pragma experimental ABIEncoderV2;

// 供应链金融平台的智能合约
contract SupplyChain {

    address private caAddr; // 部署合约的认证机构地址 
    // enum CompanyType { Financing, Core, Downstream } // 企业类型: 金融机构 / 核心企业 / 下游企业

    struct Company{
        string companyName; // 企业名称
        int balance;         // 账户余额
        int companyType;    // 企业类型 0 - 金融机构 1 - 核心机构 2 - 下游企业
        bool isRegistered;  // 验证企业是否存在
    }
    // 企业哈希表
    mapping(address => Company) private companyMap;

    struct Receipt {
        address from;       // 发起方地址
        address to;         // 接收方地址
        int amount;         // 债权凭证金额
        bool isSettled;     // 账单状态: 已结算 / 待结算 
    }
    // 债权凭证列表
    Receipt[] private receiptList;

    constructor() public {
        caAddr = msg.sender;
    }

    // 认证机构为一个企业进行注册
    function registerCompany(address companyAddr, string memory companyName, int balance, int companyType) 
        public returns(bool) {
        
        // require(msg.sender == caAddr, "[registerCompany]: Certification Authority Only");
        if(msg.sender != caAddr) {
            return false;
        }

        Company storage newCompany = companyMap[companyAddr];
        if(newCompany.isRegistered == true) {
            return false;
        }
        else{
            newCompany.companyName = companyName;
            newCompany.balance = balance;
            newCompany.companyType = companyType;
            newCompany.isRegistered = true;
            return true;
        }
    }

    // 查询企业信息
    function getCompanyInfo(address addr) public view returns(Company memory) {
        Company storage company = companyMap[addr];
        // require(company.isRegistered == true, "[getCompanyInfo]: Company is not registered");
        return company;
    }

    // 企业查询所有收账账单
    function getCompanyReceipts(address addr, bool containHistory) public view returns(Receipt[] memory) {
        Company storage company = companyMap[addr];
        // require(company.isRegistered == true, "[getCompanyReceipts]: Company is not registered");
        uint count = 0;
        for(uint i = 0; i < receiptList.length; i++) {
            if(receiptList[i].to == addr) {
                if(containHistory || !receiptList[i].isSettled){
                    count++;
                }
            }
        }
        
        Receipt[] memory rec = new Receipt[](count);
        count = 0;
        for(uint i = 0; i < receiptList.length; i++) {
            if(receiptList[i].to == addr) {
                if(containHistory || !receiptList[i].isSettled){
                    rec[count++] = receiptList[i];
                }
            }
        }
        return rec;
    }

    // 企业查询所有负债账单
    function getCompanyDebts(address addr, bool containHistory) public view returns(Receipt[] memory) {
        Company storage company = companyMap[addr];
        // require(company.isRegistered == true, "[getCompanyDebts]: Company is not registered");
        uint count = 0;
        for(uint i = 0; i < receiptList.length; i++) {
            if(receiptList[i].from == addr) {
                if(containHistory || !receiptList[i].isSettled){
                    count++;
                }
            }
        }
        
        Receipt[] memory rec = new Receipt[](count);
        count = 0;
        for(uint i = 0; i < receiptList.length; i++) {
            if(receiptList[i].from == addr) {
                if(containHistory || !receiptList[i].isSettled){
                    rec[count++] = receiptList[i];
                }
            }
        }
        return rec;
    }

    // 企业查询待结算收账账单总额
    function getPendingReceiptsAmount() public view returns(int) {
        Company storage company = companyMap[msg.sender];
        // require(company.isRegistered == true, "[getPendingReceipts]: Company is not registered");
        if(!company.isRegistered){
            return 0;
        }

        int totalAmount = 0;
        for(uint i = 0; i < receiptList.length; i++) {
            if(receiptList[i].to == msg.sender && !receiptList[i].isSettled) {
                totalAmount += receiptList[i].amount;
            }
        }
        return totalAmount;
    }  

    // 企业查询待结算负债账单总额
    function getPendingDebtsAmount() public view returns(int) {
        Company storage company = companyMap[msg.sender];
        // require(company.isRegistered == true, "[getPendingDebts]: Company is not registered");
        if(!company.isRegistered){
            return 0;
        }

        int totalAmount = 0;
        for(uint i = 0; i < receiptList.length; i++) {
            if(receiptList[i].from == msg.sender && !receiptList[i].isSettled) {
                totalAmount += receiptList[i].amount;
            }
        }
        return totalAmount;
    } 

    // 功能一：应收账款交易上链
    function createReceipt(address to, int amount) public returns(bool) {
        Company storage company = companyMap[msg.sender];
        Company storage companyTo = companyMap[to];
        // require(company.isRegistered == true && companyTo.isRegistered == true, "[createReceipt]: Company is not registered");
        // require(company.companyType == CompanyType.Core || company.companyType == CompanyType.Financing, "[createReceipt]: Core/Financing Company Only");
        if(!company.isRegistered || !companyTo.isRegistered) {
            return false;
        }
        else if(company.companyType != 1 && company.companyType != 2){
            return false;
        }

        receiptList.push(
            Receipt({
                from: msg.sender,
                to: to,
                amount: amount,
                isSettled: false
            })
        );

        company.balance += amount;

        return true;
    }

    // 功能二：应收账款的转让上链
    function transferReceipt(address to, int amount) public returns(bool) {
        Company storage company = companyMap[msg.sender];
        Company storage companyTo = companyMap[to];
        // require(company.isRegistered == true && companyTo.isRegistered == true, "[transferReceipt]: Company is not registered");
        if(!company.isRegistered || !companyTo.isRegistered) {
            return false;
        }

        if(getPendingReceiptsAmount() < amount) {
            return false;
        }
        
        int restAmount = amount;
        for(uint i = 0; i < receiptList.length; i++) {
            if(receiptList[i].to == msg.sender && !receiptList[i].isSettled) { // 直接转移账单接收方
                if(receiptList[i].amount <= restAmount) {
                    receiptList[i].to = to;
                    restAmount -= receiptList[i].amount;

                    if(restAmount == 0) {
                        break;
                    }
                }
                else { // 拆分一个账单的金额
                    receiptList[i].amount -= restAmount;

                    receiptList.push(
                        Receipt({
                            from: receiptList[i].from,
                            to: to,
                            amount: restAmount,
                            isSettled: false
                        })
                    );
                    break;
                }
            }
        }
        return true;
    }

    // 功能三: 利用应收账款向银行融资上链
    function applyFinancing(address to, int amount) public returns(bool) {
        Company storage company = companyMap[msg.sender];
        Company storage companyTo = companyMap[to];
        // require(company.isRegistered == true && companyTo.isRegistered == true, "[applyFinancing]: Company is not registered");
        // require(companyTo.companyType == CompanyType.Financing, "[applyFinancing]: Destination is not Financing Authority");
        if(!company.isRegistered || !companyTo.isRegistered) {
            return false;
        }
        else if(company.companyType != 3){
            return false;
        }

        if(companyTo.balance < amount) { // 银行没钱
            return false;
        }
        
        if(transferReceipt(to, amount)) {
            company.balance += amount;
            companyTo.balance -= amount;
            return true;
        }
        else{ // 待结算收账账单总额申请不了这么多钱
            return false;
        }
    }

    // 功能四: 应收账款支付结算上链
    function settleReceipt() public returns(bool) {
        Company storage company = companyMap[msg.sender];
        // require(company.isRegistered == true, "[settleReceipt]: Company is not registered");
        if(!company.isRegistered) {
            return false;
        }

        int totalDebt = getPendingDebtsAmount();
        if(company.balance < totalDebt) { // 不够还钱
            return false;
        }
        
        for(uint i = 0; i < receiptList.length; i++) {
            if(receiptList[i].from == msg.sender && !receiptList[i].isSettled) {
                companyMap[receiptList[i].to].balance += receiptList[i].amount;
                receiptList[i].isSettled = true;
            }
        }
        company.balance -= totalDebt;
        return true;
    }
}
