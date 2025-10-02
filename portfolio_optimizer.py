#!/usr/bin/env python3
from __future__ import annotations
import random
import math
import json
from typing import List, Dict, Any

class Asset:
    def __init__(self, name: str, expected_return: float, volatility: float):
        self.name = name
        self.expected_return = expected_return
        self.volatility = volatility

class Portfolio:
    def __init__(self):
        self.assets: List[Asset] = []
        self.weights: Dict[str, float] = {}

    def add_asset(self, asset: Asset):
        self.assets.append(asset)
        self.weights[asset.name] = 1 / len(self.assets)

    def random_weights(self):
        r = [random.random() for _ in self.assets]
        total = sum(r)
        for i, asset in enumerate(self.assets):
            self.weights[asset.name] = r[i] / total

    def expected_return(self) -> float:
        return sum(self.weights[a.name] * a.expected_return for a in self.assets)

    def portfolio_volatility(self) -> float:
        return math.sqrt(sum((self.weights[a.name] * a.volatility) ** 2 for a in self.assets))

    def sharpe_ratio(self, risk_free: float = 0.01) -> float:
        vol = self.portfolio_volatility()
        if vol == 0:
            return 0.0
        return (self.expected_return() - risk_free) / vol

    def optimize(self, iterations: int = 1000) -> None:
        best_sr = -math.inf
        best_weights = self.weights.copy()
        for _ in range(iterations):
            self.random_weights()
            sr = self.sharpe_ratio()
            if sr > best_sr:
                best_sr = sr
                best_weights = self.weights.copy()
        self.weights = best_weights

    def to_dict(self) -> Dict[str, Any]:
        return {"weights": self.weights, "assets": [{ "name": a.name, "expected_return": a.expected_return, "volatility": a.volatility } for a in self.assets]}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Portfolio:
        p = cls()
        for a in data.get("assets", []):
            p.add_asset(Asset(a["name"], a["expected_return"], a["volatility"]))
        p.weights = data.get("weights", {})
        return p

def demo():
    portfolio = Portfolio()
    portfolio.add_asset(Asset("AAPL", 0.12, 0.2))
    portfolio.add_asset(Asset("MSFT", 0.10, 0.18))
    portfolio.add_asset(Asset("GOOG", 0.11, 0.25))
    print("Before optimization:", portfolio.weights)
    portfolio.optimize(5000)
    print("Optimized weights:", portfolio.weights)
    print("Expected return:", round(portfolio.expected_return(),4))
    print("Volatility:", round(portfolio.portfolio_volatility(),4))
    print("Sharpe ratio:", round(portfolio.sharpe_ratio(),4))

if __name__ == "__main__":
    demo()
