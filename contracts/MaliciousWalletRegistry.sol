// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MaliciousWalletRegistry {
    address public owner;
    mapping(address => bool) public flaggedAddresses;

    event WalletFlagged(address indexed wallet, string reason);
    event WalletCleared(address indexed wallet);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function flagAddress(address _wallet, string memory _reason) public onlyOwner {
        flaggedAddresses[_wallet] = true;
        emit WalletFlagged(_wallet, _reason);
    }

    function clearAddress(address _wallet) public onlyOwner {
        require(flaggedAddresses[_wallet], "Address is not flagged");
        flaggedAddresses[_wallet] = false;
        emit WalletCleared(_wallet);
    }

    function isFlagged(address _wallet) public view returns (bool) {
        return flaggedAddresses[_wallet];
    }
}
