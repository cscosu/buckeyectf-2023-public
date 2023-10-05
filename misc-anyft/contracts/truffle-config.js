require('dotenv').config()
const HDWalletProvider = require('@truffle/hdwallet-provider');

const MNEMONIC =  process.env.MNEMONIC;
const ACCESSTOKEN = process.env.ACCESSTOKEN;

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",     // Localhost (default: none)
      port: 8545,            // Standard Ethereum port (default: none)
      network_id: "*",       // Any network (default: none)
    },
  
    sepolia: {
      provider: () => new HDWalletProvider(MNEMONIC, `https://sepolia.infura.io/v3/${ACCESSTOKEN}`),
      network_id: Number(process.env.NETWORKID),       // Sepolia's id
      skipDryRun: true     // Skip dry run before migrations? (default: false for public nets )
    },
  },

  compilers: {
    solc: {
      version: "0.8.20",      
    }
  },
};
