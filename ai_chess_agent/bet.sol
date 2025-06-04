// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract BetManager {
    struct Bet {
        address bettor;
        uint256 amount;
        bool onWhite;
    }

    mapping(uint256 => Bet[]) public bets;
    address public owner;
    uint256 public feePercent = 5; // 5% fee

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function placeBet(uint256 gameId, bool onWhite) external payable {
        require(msg.value > 0, "No bet amount");
        bets[gameId].push(Bet(msg.sender, msg.value, onWhite));
    }

    function settle(uint256 gameId, bool whiteWon) external onlyOwner {
        Bet[] storage gameBets = bets[gameId];
        uint256 totalPot = 0;
        uint256 winnersPot = 0;

        // Calculate total pot and winners' pot
        for (uint256 i = 0; i < gameBets.length; i++) {
            totalPot += gameBets[i].amount;
            if (gameBets[i].onWhite == whiteWon) {
                winnersPot += gameBets[i].amount;
            }
        }

        require(winnersPot > 0, "No winners");

        uint256 fee = (totalPot * feePercent) / 100;
        uint256 payoutPot = totalPot - fee;

        // Pay winners proportionally
        for (uint256 i = 0; i < gameBets.length; i++) {
            if (gameBets[i].onWhite == whiteWon) {
                uint256 payout = (payoutPot * gameBets[i].amount) / winnersPot;
                payable(gameBets[i].bettor).transfer(payout);
            }
        }

        // Transfer fee to owner
        payable(owner).transfer(fee);

        // Clean up bets for this game
        delete bets[gameId];
    }
}