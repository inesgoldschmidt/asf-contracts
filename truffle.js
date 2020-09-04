require('dotenv').config();
var HDWalletProvider = require("truffle-hdwallet-provider");

module.exports = {
    networks: {
        development: {
            host: "localhost",
            port: 8545,
            network_id: "*", // Match any network id
            // gas: 46000000
        },
        ropsten: {
            provider: function() {
              return new HDWalletProvider(process.env.INFURA_ROPSTEN_MNEMONIC, `https://ropsten.infura.io/${process.env.INFURA_KEY}`)
            },
            network_id: "3",
            gas: 7000000, // Gas limit used for deploys
            gasPrice: 40000000000
        },
        kovan: {
            provider: function() {
              return new HDWalletProvider(process.env.INFURA_KOVAN_MNEMONIC, `https://kovan.infura.io/${process.env.INFURA_KEY}`)
            },
            network_id: "42",
            gas: 2000000, // Gas limit used for deploys
            gasPrice: 3000000000
        },
        main: {
            provider: function() {
              return new HDWalletProvider(process.env.INFURA_MAINNET_MNEMONIC, `https://mainnet.infura.io/${process.env.INFURA_KEY}`)
            },
            network_id: "1",
            gasPrice: 20000000000, // Be careful, this is in Shannon
            gas: 6000000 // Gas limit used for deploys
        },
    	coverage: {
    	    host: "localhost",
    	    port: 8555,
            network_id: "*",
            gas: 46000000
    	}
    },
    // Configure your compilers
    compilers: {
        solc: {
            version: "0.4.24",    // Fetch exact version from solc-bin (default: truffle's version)
            settings: {          // See the solidity docs for advice about optimization and evmVersion
                optimizer: {
                    enabled: false,
                    runs: 1
                },
            }
        },
    },
};
