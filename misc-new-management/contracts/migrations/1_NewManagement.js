var newManagement  = artifacts.require("NewManagement");

module.exports = function(deployer) {
  deployer.deploy(newManagement);
};