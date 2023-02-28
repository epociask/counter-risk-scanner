# (CSR) Counter Risk Scanner

Dynamic/Static analysis on tokenized assets (ERC-20, ERC-721) for counter-party and market related risks. 

__Please see [FRAMEWORK.md](./FRAMEWORK.md) to understand risk methodology & classification procedures__

## To Setup
1. Create yout `config.env` file.
```
mv .config.env config.env
```

2.  Populate your `config.env` with relevant API keys.
* Etherscan API keys can be obtained through creating an explorer [account](https://etherscan.io/login) and generating an API key.

* Node RPC endpoints can be created using node provider applications like [infura](https://www.infura.io/) or [alchemy](https://www.alchemy.com/).

3. Install relevant python dependencies:
```
pip3 install -r requirements.txt
```

## To Run
```
python3 main.py -a "0xDEADBEEF" -n "eth"
```
