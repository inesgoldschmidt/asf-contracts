var AppCoins = artifacts.require("./AppCoins.sol");
var Shares = artifacts.require("./lib/Shares.sol");
var AdvertisementStorage = artifacts.require("./AdvertisementStorage.sol");
var AdvertisementFinance = artifacts.require("./AdvertisementFinance.sol");
var Advertisement = artifacts.require("./Advertisement.sol");

require('dotenv').config();

module.exports = async function(deployer, network) {
    switch (network) {
        case 'coverage':
        case 'development':
            deployer.link(Shares, Advertisement);
            deployer.deploy(Advertisement, AppCoins.address, AdvertisementStorage.address,AdvertisementFinance.address);
            // AppCoins.deployed()
            // .then(function() {
            //     return AdvertisementStorage.deployed()
            // })
            // .then(function() {
            //     return AdvertisementFinance.deployed()
            // }).then( async function() {
            //     await deployer.link(Shares, Advertisement);
            //     return deployer.deploy(Advertisement, AppCoins.address, AdvertisementStorage.address,AdvertisementFinance.address);
            // });

            break;

        case 'ropsten':
            AppCoinsAddress = process.env.APPCOINS_ROPSTEN_ADDRESS;
            AdvertisementFinanceAddress =  process.env.ADVERTISEMENT_FINANCE_ROPSTEN_ADDRESS;
            AdvertisementStorageAddress = process.env.ADVERTISEMENT_STORAGE_ROPSTEN_ADDRESS;

            if(!AppCoinsAddress.startsWith("0x")) {
                throw 'AppCoins Address not found!'
            }

            if (!AdvertisementFinanceAddress.startsWith("0x") || !AdvertisementStorageAddress.startsWith("0x")) {
                AdvertisementStorage.deployed()
                .then(function() {
                    return AdvertisementFinance.deployed()
                })
                .then(function() {
                    return Shares.deployed()
                })
                .then(async function() {
                    await deployer.link(Shares, Advertisement);
                    return deployer.deploy(Advertisement, AppCoins.address, AdvertisementStorage.address,AdvertisementFinance.address);
                });

            } else {
                Shares.deployed().then(function() {
                    deployer.link(Shares, Advertisement).then(function() {
                        deployer.deploy(Advertisement, AppCoinsAddress, AdvertisementStorageAddress, AdvertisementFinanceAddress);
                    })
                })
            }

            break;

        case 'kovan':
            AppCoinsAddress = process.env.APPCOINS_KOVAN_ADDRESS;
            AdvertisementFinanceAddress =  process.env.ADVERTISEMENT_FINANCE_KOVAN_ADDRESS;
            AdvertisementStorageAddress = process.env.ADVERTISEMENT_STORAGE_KOVAN_ADDRESS;

            if(!AppCoinsAddress.startsWith("0x")) {
                throw 'AppCoins Address not found!'
            }

            if (!AdvertisementFinanceAddress.startsWith("0x") || !AdvertisementStorageAddress.startsWith("0x")) {
                AdvertisementStorage.deployed()
                .then(function() {
                    return AdvertisementFinance.deployed()
                })
                .then(function() {
                    return Shares.deployed()
                })
                .then(async function() {
                    await deployer.link(Shares, Advertisement);
                    return deployer.deploy(Advertisement, AppCoins.address, AdvertisementStorage.address,AdvertisementFinance.address);
                });

            } else {
                await deployer.link(Shares, Advertisement);
                deployer.deploy(Advertisement, AppCoinsAddress, AdvertisementStorageAddress, AdvertisementFinanceAddress);
            }

            break;

        case 'main':

            AppCoinsAddress = process.env.APPCOINS_MAINNET_ADDRESS;
            AdvertisementFinanceAddress =  process.env.ADVERTISEMENT_FINANCE_MAINNET_ADDRESS;
            AdvertisementStorageAddress = process.env.ADVERTISEMENT_STORAGE_MAINNET_ADDRESS;

            if(!AppCoinsAddress.startsWith("0x")) {
                throw 'AppCoins Address not found!'
            }

            if (!AdvertisementFinanceAddress.startsWith("0x") || !AdvertisementStorageAddress.startsWith("0x")) {
                AdvertisementStorage.deployed()
                .then(function() {
                    return AdvertisementFinance.deployed()
                })
                .then(function() {
                    return Shares.deployed()
                })
                .then(async function() {
                    await deployer.link(Shares, Advertisement);
                    return deployer.deploy(Advertisement, AppCoins.address, AdvertisementStorage.address,AdvertisementFinance.address);
                });

            } else {
                Shares.deployed().then(function() {
                    deployer.link(Shares, Advertisement).then(function() {
                        deployer.deploy(Advertisement, AppCoinsAddress, AdvertisementStorageAddress, AdvertisementFinanceAddress);
                    })
                })
            }

            break;

        default:
            throw `Unknown network "${network}". See your Truffle configuration file for available networks.` ;

    }
};
