var aNyFT = artifacts.require("aNyFT");

module.exports = function(deployer) {
  deployer.deploy(aNyFT, "aNyFT", "aNyFT");
};